# Home Assistant Smart Covers Integration

Intelligent Home Assistant integration for automated cover control with time-based scheduling, weather protection, and precise positioning. Designed to effortlessly manage your covers, syncing with your chosen entities for raising and lowering. Plus, it remembers your settings after restarts and supports tilting.

## How to Install

Getting started is a piece of cake!

You can simply copy all files from the custom_components/smart_covers directory into your Home Assistant's /custom_components/smart_covers/ directory.

Then, just give Home Assistant a quick restart, and you're good to go.

## Setting Things Up

Head over to Settings -> Devices and Services -> Click on Add Integration (select Smart Covers) to integrate your covers into the system.

Name your cover, select the controlling entities, specify roll-up and roll-down times in seconds, and if you need it, set tilt times (or leave them at 0 if you don't want tilt support).

Once everything is set up, the calculations will indicate that the cover is fully closed. Therefore, after configuring, <span style="color:red">wait</span> before submitting, move your cover to the closed position, and then submit.

You can also tweak existing configurations to suit your preferences (just reload the edited entries).

## Automations

During the setup process, you have the option to configure various automated tasks. These features are currently in an <span style="color:red">EXPERIMENTAL</span> phase and are being developed as part of my bachelor's thesis, so please refrain from extensive experimentation with this automation.

Examples include scheduling specific times for actions such as opening or closing covers, automating the opening and closing of covers based on sunrise and sunset times, or automatically closing covers when a particular entity is activated during the night. Additionally, there are weather protection measures available, such as responding to strong winds using the [WMO Code](https://www.nodc.noaa.gov/archive/arc0021/0002199/1.1/data/0-data/HTML/WMO-CODE/WMO4677.HTM) and utilizing the [Open Meteo API](https://open-meteo.com/) or perhaps you would like to use [Netatmo](https://open-meteo.com/), that also works. For those utilizing interlock relays, there's the possibility of triggering a stop command at the end of travel.
