"""Compatibility entry point for the current all-code delivery review (never accepts holds)."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[5]/'tools'))
from check_sign_delivery import main
if __name__=='__main__':main()
