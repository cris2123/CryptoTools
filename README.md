#### Project Name: CryptoTools


##### Description

A suit of parsers and API calls to notorious websites where we can analyze cryptocurrencies trends and get news about cryptocurrencies and investment

##### Table of contents:

[Installation](#installation)

##### Installation

This file has to be executed from the terminal. The first thing to do is to download the repository from Github.

There we will give execution rights to the user that will use the program with the following command:

`chmod +x main.py`

Then we have to create a folder in the home directory, if necessary.

`mkdir ~/.bin`

Now we need to create a symbolic link with the following command:

`ln -s $HOME/where_do_you_download_repo/main.py $HOME/.bin/CryptoTools`

Also we need to add the directory path where the executables of CryptoTools will be stored. We do this by using nano:

`nano ~/.bashrc`

Then we add the following line:

`export PATH=$PATH:$HOME/.bin`

The last command for the installation is:

`source ~/.bashrc`

[Usage](#usage)

##### Usage

To use CryptoTools we write the following command:
CryptoTools -c coinName

For example, if we want to get the current value of Steem we write:

`CryptoTools -c SBD`


In case we want to obtain the value relative to an alternative fiat we write:

`CryptoTools -c SBD -f EUR`


With the following command we can obtain the criptocurrencies' global Market Cap:

`CryptoTools -g True`


We can give a list of cryptocurrencies as input:

`CryptoTools -cl SBD Ethereum Bitcoin ADA Monero -f BRL`

The parameter `-w` can be provided as input to select what parser will be used for the different cryptocurrencies websites (not implemented yet).


<a name="contributing"/>

##### Contributing

Feel free to contribute by forking the GitHub Repo. Create a branch and make all the changes that you want. After finishing your changes create a pull request. Please provide detailed information for contributors about you and how they can get in touch with you.


<a name="credits"/>

##### Credits

Author: Cristhian Bravo.

Contributors:
