#!/usr/bin/env python3

import os
import sys
import json
import requests
from typing import Dict, Any

def make_graphql_request(query: str, variables: Dict[str, Any], token: str) -> Dict[str, Any]:
    """Make a GraphQL request to Railway API"""
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        
        response = requests.post(
            'https://backboard.railway.app/graphql/v2',
            headers=headers,
            json={'query': query, 'variables': variables},
            timeout=30  # Add timeout
        )
        
        if response.status_code != 200:
            print(f"Error: HTTP {response.status_code}")
            print(response.text)
            sys.exit(1)
            
        result = response.json()
        
        if 'errors' in result:
            print("GraphQL Errors:")
            for error in result['errors']:
                print(f"- {error.get('message', 'Unknown error')}")
                if 'extensions' in error:
                    print(f"  Details: {json.dumps(error['extensions'], indent=2)}")
            sys.exit(1)
            
        return result
    except requests.exceptions.Timeout:
        print("❌ Request timed out while connecting to Railway API")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error occurred: {str(e)}")
        sys.exit(1)
    except json.JSONDecodeError:
        print("❌ Failed to parse API response")
        print("Response:", response.text)
        sys.exit(1)

def deploy_image() -> None:
    """Main deployment function"""
    required_env_vars = [
        'AUTHORIZATION_TOKEN',
        'IMAGE_URL',
        'SERVICE_ID',
        'ENVIRONMENT_ID'
    ]
    
    # Validate environment variables
    for var in required_env_vars:
        if not os.getenv(var):
            print(f"Error: {var} environment variable is required")
            sys.exit(1)
    
    token = os.getenv('AUTHORIZATION_TOKEN')
    image_url = os.getenv('IMAGE_URL')
    service_id = os.getenv('SERVICE_ID')
    environment_id = os.getenv('ENVIRONMENT_ID')
    
    # GraphQL mutation
    query = """
    mutation serviceInstanceUpdate(
        $environmentId: String!,
        $input: ServiceInstanceUpdateInput!,
        $serviceId: String!
    ) {
        update: serviceInstanceUpdate(
            environmentId: $environmentId,
            input: $input,
            serviceId: $serviceId
        )
        deploy: serviceInstanceDeploy(
            environmentId: $environmentId,
            serviceId: $serviceId
        )
    }
    """
    
    variables = {
        "environmentId": environment_id,
        "input": {
            "source": {
                "image": image_url
            },
            "multiRegionConfig": {
                "regions": {
                    "us-west1": {}
                }
            },
            "region": "us-west1"
        },
        "serviceId": service_id
    }
    
    print(f"Deploying image {image_url} to Railway service {service_id}")
    
    try:
        result = make_graphql_request(query, variables, token)
        if result.get('data', {}).get('update') and result.get('data', {}).get('deploy'):
            print("✅ Deployment initiated successfully")
        else:
            print("❌ Deployment failed")
            print("Response:", json.dumps(result, indent=2))
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error during deployment: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    deploy_image() 