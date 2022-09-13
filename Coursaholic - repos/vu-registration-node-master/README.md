**IT IS NOT IN YOUR INTEREST TO SHARE THIS SCRIPT. IF YOU DO, I WILL ~~PERSONALLY~~ HAVE SOMEONE BEAT YOU UP. -Yunyu**

*If you are enrolled in a graduate program, please follow the [graduate instructions](https://github.com/yunyu/vu-registration-node/blob/master/GRAD_INSTRUCTIONS.md), and then return to this document.*

Install
==

This script requires [Node.js](https://nodejs.org/en/), and the minimum supported version is 8.x (LTS release). First `cd` into the script directory, and then run:

    npm install

Then follow the usage instructions below for your shell.

Finding class numbers
==

To find a class number, click the course name in your cart, and look at the upper left corner (underneath the description):

![](https://i.imgur.com/nxVkT27.png)

Usage
==

Bash:

```bash
export VUNET_ID='liny19'
export VUNET_PW='password'
node vu-registration.js savecookies
node vu-registration.js register 0049:true,0050:true
```

PowerShell:

```powershell
$env:VUNET_ID = "liny19"
$env:VUNET_PW = "password"
node vu-registration.js savecookies
# The second parameter needs to be quoted in PowerShell
node vu-registration.js register "0049:true,0050:true"
```

For complete usage instructions, run `node vu-registration.js` with no arguments. Be sure to run `node vu-registration.js savecookies` about 3 minutes before registration opens.

Credits
==

* Winston Du for developing registration method
* Yunyu Lin for user interface and node project development
* Matthew Sedam for node project development
* Ben Cooper for node project development
* Sameer Puri for node project development
* Oishik Ray for PowerShell automation
