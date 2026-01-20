#!/usr/bin/env python3
"""
Generate Polymarket CLOB API Key using py_clob_client

This script creates API credentials for accessing the Polymarket CLOB API.
It requires a wallet private key in the .env file.

Documentation: https://docs.polymarket.com/developers/CLOB/clients/methods-l1
"""
import asyncio
import os
import sys
from pathlib import Path
from py_clob_client.client import ClobClient
from dotenv import load_dotenv

# Add project root to path to ensure modules can be imported if needed
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv()

async def generate_api_key():
    """Generate Polymarket CLOB API credentials"""
    print("🔑 Generating Polymarket CLOB API Key...\n")

    # Check if private key exists
    private_key = os.getenv("PRIVATE_KEY")
    if not private_key:
        print("❌ Error: PRIVATE_KEY not found in .env file")
        print("\nPlease add your private key to the .env file:")
        print("PRIVATE_KEY=0x...\n")
        sys.exit(1)

    # Ensure private key has 0x prefix
    if not private_key.startswith("0x"):
        print("ℹ️  Adding '0x' prefix to private key")
        private_key = "0x" + private_key

    try:
        # Create CLOB client
        print("📝 Creating CLOB client...")
        # Note: Depending on account status, this might fail immediately or later
        client = ClobClient(
            host="https://clob.polymarket.com",
            chain_id=137,  # Polygon mainnet
            key=private_key
        )
        print("   Connected to Polymarket CLOB\n")

        # Generate API key
        print("🔐 Creating API credentials...")
        
        try:
            api_creds = await client.create_api_key()
            
            print("\n✅ SUCCESS! API Key created successfully!\n")
            print("═" * 60)
            print("API Credentials:")
            print("═" * 60)
            print(f"API Key:    {api_creds['apiKey']}")
            print(f"Secret:     {api_creds['secret']}")
            print(f"Passphrase: {api_creds['passphrase']}")
            print("═" * 60)
            
            # Note: We don't automatically save to .env to avoid overwriting existing config
            # without user permission, but we output it clearly.
            print("\nPlease add these to your .env file:\n")
            print(f"CLOB_API_KEY={api_creds['apiKey']}")
            print(f"CLOB_SECRET={api_creds['secret']}")
            print(f"CLOB_PASSPHRASE={api_creds['passphrase']}")

        except Exception as e:
            print(f"\n❌ FAILED to create API Key:")
            print(f"   {str(e)}")
            if "400" in str(e):
                print("\nPossible causes:")
                print("1. Wallet needs to be initialized (try logging in on polymarket.com first)")
                print("2. Wallet needs a small amount of MATIC")
                print("3. System time is out of sync")

    except Exception as e:
        print(f"\n❌ Error initializing client: {e}")
        
if __name__ == '__main__':
    asyncio.run(generate_api_key())
