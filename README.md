# Loadshedding Notifier
### Backstory:

Hello World, my name is Gareth and I am 17 living in South Africa. In South Africa there is one major power company that powers the entire country that goes by the name of **Eskom**. Ever since 2014 they implemented "loadshedding" which according to wikipedia is defined as 

> "load shedding is implemented whenever generating units are taken offline for maintenance, repairs or re-fueling (in the case of nuclear units)"

This happens and still continues to happen to this day because Eskom is not capable of producing enough electricity for all of their customers and is forced to cut the power to certain areas according to a schecule when they anounce that loadshedding is active. The length of the power cuts are usually 2 hours long and the frequency per day depends on the level of loadshedding at that time.

### What is it?

The main version of this software was designed to run on a raspberry pi in an infinite loop checking if the power is going to go off and only stopping when it shuts itself down 5 minutes before. I made it to work in the background connected to a speaker with the only intention being to play me an audio cue giving me sufficient warning before hand so I don't lose any work or damage any of my components or data.

### How does it work?

It was designed to open the website that shows the status and the times of loadshedding and automaticly read the status and fill in the locational data on the web form on the site to display the times that need to be extracted. It then checks this collected data and prints out the time until the powercut in the terminal and the log file, but if the status shows that there is no active loadshedding at the moment it will do nothing and wait a while before checking the website again.

- For filling in web forms `selenium` was used
- For selecting the location from the dropdown `pynput` was used
- `lxml`, `requests` and `selenium.webdriver` where used in web scraping

### Reasoning:

The reason I decided to make a form of audible notification was because there have been many times where I just haven't been by my phone to see the schedule or it is out of battery and I continue to use my devices as usual not knowing that Eskom has enounced that loadshedding it taking place soon. Unknowingly, I continue to work or play and find myself caught in the dark losing all the data that I didn't save and worrying if the more fragile computers like the Rasperry Pi will even be able to boot again due to corruption. I knew I needed a final project so I decided to have the Pi run all the time constantly checking and telling me when the powers about to go out.

## Disclaimer!

This program was writen with regards to my own person situation in mind and your setup and/or experience may differ if you choose to use this project for yourself

## Concerning Windows Users:

As you can see from the contents of the repository there is a version of the program for **Windows** that I am working on that will shutdown your computer before the power goes out. This has not been completed as it still contains bugs and is probably not going to work if you try and use it. __So don't__

### More information:

If you would like to read more about the power crisis in South Africa and more about what loadshedding is you can take a glance at Eskom's official site that can be found [here](https://loadshedding.eskom.co.za/loadshedding/description).