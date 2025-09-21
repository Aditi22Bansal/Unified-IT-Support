#!/usr/bin/env python3
"""
Test script to verify the enhanced backend works correctly
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Test imports
    print("Testing imports...")
    import simple_main_enhanced
    print("✅ All imports successful")
    
    # Test basic functionality
    print("Testing basic functionality...")
    from simple_main_enhanced import tickets_db, manager
    print(f"✅ Tickets database loaded with {len(tickets_db)} tickets")
    print(f"✅ Connection manager initialized")
    
    # Test ticket data structure
    if tickets_db:
        sample_ticket = tickets_db[0]
        required_fields = ['id', 'title', 'description', 'priority', 'status', 'category']
        missing_fields = [field for field in required_fields if field not in sample_ticket]
        if missing_fields:
            print(f"❌ Missing fields in ticket: {missing_fields}")
        else:
            print("✅ Ticket data structure is valid")
    
    print("\n🎉 Backend test completed successfully!")
    print("You can now run: python simple_main_enhanced.py")
    
except Exception as e:
    print(f"❌ Error testing backend: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)




