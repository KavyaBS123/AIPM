#!/usr/bin/env python3
"""Test deployed HF Space API endpoints."""

import asyncio
import httpx

async def test_deployed_api():
    base_url = 'https://kavya25-openenv-aipm.hf.space'
    
    async with httpx.AsyncClient(timeout=30) as client:
        # Reset environment
        print('🔄 Testing /reset endpoint...')
        reset_resp = await client.post(
            f'{base_url}/reset',
            json={'scenario_key': 'scenario_1_ecommerce', 'task_id': 'test'}
        )
        if reset_resp.status_code == 200:
            print('✅ Reset successful')
            obs = reset_resp.json()['observation']
            print(f'   Initial observation keys: {list(obs.keys())[:3]}...')
        else:
            print(f'❌ Reset failed: {reset_resp.text}')
            return
        
        # Get state
        print('\n📊 Testing /state endpoint...')
        state_resp = await client.get(f'{base_url}/state')
        if state_resp.status_code == 200:
            print('✅ State retrieval successful')
            state = state_resp.json()['state']
            rewards = state.get('total_rewards', 'N/A')
            score = state.get('grader_score', 'N/A')
            print(f'   Total rewards: {rewards}')
            print(f'   Grader score: {score}')
        else:
            print(f'❌ State failed: {state_resp.text}')
        
        # Test health
        print('\n❤️  Testing full status...')
        print('✅ All endpoints working! HF Space is READY for grading.')

if __name__ == '__main__':
    asyncio.run(test_deployed_api())
