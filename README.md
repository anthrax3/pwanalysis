# Password Analysis: PWAnalysis
This project provides a set of tools for analyzing password dumps. It is extensible and includes a dynamic module loader 
to include further analysis modules. A description on module creation and addition is included in this readme.

```
usage: pwanalysis.py [-h] [--userpass USERPASS] [--pw PW] [-v] [--block BLOCK]

optional arguments:
  -h, --help           show this help message and exit
  --userpass USERPASS  A file that contains the usernames and passwords (in
                       the standard <user>:<pass> format) on each line
  --pw PW              A file that contains a password on each line
  -v, --verbose        Verbose output mode
  --block BLOCK        Block (chunk) size to read from file at a time (for
                       memory optimization) (Default: 10000)

examples
  python pwanalysis.py --userpass resources/userpass.dump
  python pwanalysis.py --pw resources/ptxt_passwords.dump
```

## Built-In Modules
The basic modules of this tool include the following:
* N-Gram Frequency Analysis (Status: Working)
* Username-Password Comparison (Status: Incomplete)

### N-Gram Frequency Analysis
Status: Working

The N-Gram Frequency Analysis module takes either a list of usernames and passwords (file in <user>:<pass> format per 
line) or a list of passwords (file in <pass> format per line). Each string is broken down into all possible n-grams and 
their frequencies calculated and aggregated. 

Output: The top 10 n-grams are currently printed for each n-gram size.

### Username-Password Comparison
Status: Incomplete

The Username-Password Comparison module analyzes the <user>:<pass> pairs and identifies similarities between them.

Output: The top n-grams that are common in both usernames and associated passwords

## Adding Modules
PWAnalysis is extensible in that other modules can be created and loaded into the engine.

All modules must inherit from the `analytics.base.AnalysisModuleTemplate` class and override the two functions 
`analyze_userpass` and `analyze_pass`. Their return types must be dictionary.

The engine loads modules from the FUNCTIONS class in the settings file.

To add a module to settings:  
1. Create a name (Ex: FREQ_ANALYSIS = 'Frequency Analysis')
2. Add your named variable to the module list that it applies to (Ex: USER_PASS_MODULES, etc.)
3. Add your module name and path to the MODULES dictionary



