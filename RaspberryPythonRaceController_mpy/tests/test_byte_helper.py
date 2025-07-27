"""
Test script for ByteHelper functionality
"""
import sys
sys.path.append('..')

from byte_helper import ByteHelper

def test_bit_operations():
    """Test bit manipulation operations"""
    print("Testing bit operations...")
    
    helper = ByteHelper()
    
    # Test setting bits
    helper.set_bit(0, 1)
    assert helper.get_bit(0) == True, "Bit 0 should be set"
    
    helper.set_bit(7, 1)
    assert helper.get_bit(7) == True, "Bit 7 should be set"
    
    helper.set_bit(0, 0)
    assert helper.get_bit(0) == False, "Bit 0 should be cleared"
    
    print("✓ Bit operations test passed")

def test_car_speed():
    """Test car speed setting"""
    print("Testing car speed setting...")
    
    helper = ByteHelper()
    helper.set_car_speed(10)
    
    # Speed should be XORed with current value
    expected = 0 ^ 10
    assert helper.number == expected, f"Expected {expected}, got {helper.number}"
    
    print("✓ Car speed test passed")

def test_ones_complement():
    """Test one's complement operation"""
    print("Testing one's complement...")
    
    helper = ByteHelper()
    helper.set_number(0x55)  # 01010101
    
    complement = helper.get_int_ones_complement()
    expected = 0x55 ^ 0xFF  # Should be 10101010 = 0xAA
    
    assert complement == expected, f"Expected {expected:02X}, got {complement:02X}"
    
    print("✓ One's complement test passed")

def test_crc8():
    """Test CRC8 calculation"""
    print("Testing CRC8 calculation...")
    
    # Test with known data
    test_data = [255, 255, 255, 255, 255, 255, 255, 0]
    crc = ByteHelper.crc8(test_data)
    
    # CRC should be consistent
    assert isinstance(crc, int), "CRC should be integer"
    assert 0 <= crc <= 255, "CRC should be valid byte value"
    
    # Test consistency
    crc2 = ByteHelper.crc8(test_data)
    assert crc == crc2, "CRC should be consistent"
    
    print(f"✓ CRC8 test passed (CRC: {crc})")

def run_all_tests():
    """Run all ByteHelper tests"""
    print("=== ByteHelper Tests ===")
    
    try:
        test_bit_operations()
        test_car_speed()
        test_ones_complement()
        test_crc8()
        
        print("\n✅ All ByteHelper tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    run_all_tests()