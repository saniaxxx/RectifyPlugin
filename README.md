# CraftBeerPi RectifyPlugin
This plugin allows you to use CraftBeerPi to automate the process of rectification and distillation.  
The algorithm is based on auto-reducing the collection depending on the temperature inside the pot still.  
For this, 2 modes are implemented - heads and hearts.
###### Heads:
- You specify the quantity of fraction and the speed of collection.
###### Hearts:
You should specify several parameters:
- Completion temperature, Celsius  - default 93 celsius
- Initial collecting, ml/h - as a rule, 1000 ml per 1 kW of heater power supplied

There are basic parameters for both modes:
- Collecting Actor - I use solenoid plastic valve
- Collecting indicator - for visual control of the collecting speed

![interface](https://i.ibb.co/vdfbL15/2020-01-12-19-12-13.png)
![my column](https://i.ibb.co/wsKtndK/column.jpg)
