# usragnt
This tool extracts the [User Agent](https://51degrees.com/blog/understanding-user-agent-string) field from [Zeek](https://docs.zeek.org/en/master/about.html) http.log logs, passes it to [useragentstrings.com](https://useragentstring.com/)'s API and returns the browser and its version and the OS and its version aswell. A test file named `http.log` has been provided for testing


### Useage
```bash
python3 usragnt.py {path/to/logfile}
```
---
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
