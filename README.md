# 7402_asn2
A python based implementation to break a transposition cipher

## Usage

```
usage ./transbreak.py encrypt <key> /path/to/input /path/to/output
usage ./transbreak.py decrypt <key> /path/to/input /path/to/output
usage ./transbreak.py break /path/to/ciphertext /path/to/dictionary
    to generate a dictionary the following can be used:
        aspell dump master | grep -v "'" -E '.{5,}' > dict
```