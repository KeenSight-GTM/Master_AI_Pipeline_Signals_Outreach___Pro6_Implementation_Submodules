#!/usr/bin/env python3
from pathlib import Path
import json
from keensight_contracts.validation import Bundle
if __name__=='__main__':
    result=Bundle(Path(__file__).resolve().parent).validate()
    print(json.dumps(result,indent=2,sort_keys=True))
