# Tom.Camp Data

_Tom.Camp Data_ displays data from sensors and devices from around our home and yard.
In the left hand navigation bar you will find a list of devices.

Click on a device to see the data it has collected.


This site is built using [Streamlit](https://streamlit.io/) and
the Git repo for it can be found [on Github](https://github.com/Tom-Camp/fe).

## Devices

### <a href="Germinator" target="_self">The Germinator</a>

The Germinator controls a bank of LEDs in different wavelengths to encourage
germination and solid root development. It also monitors the temperature and
humidity of the germination chamber. It is controlled by a
[Raspberry Pi Pico 2W](https://vilros.com/products/raspberry-pi-pico-2w?src=raspberrypi),
a [capacitive soil sensor](https://www.adafruit.com/product/4026), an
[AHT20 temperature and humidity sensor](https://www.adafruit.com/product/4566),
and 4 banks of [256 LEDs](https://www.aliexpress.us/item/3256803715519232.html)
in different wavelengths.

### <a href="NuLayInn" target="_self">The NuLay Inn</a>

The NuLay Inn is used to track the environment within our chicken coop. It uses
a [Adafruit Feather RP2040 RFM95](https://www.adafruit.com/product/5714) to send
data over a [LoRa](https://circuitdigest.com/article/introduction-to-lora-and-lorawan-what-is-lora-and-how-does-it-work)
network. The NuLay checks the temperature and humidity inside and outside the coop, as well as checking for
volatile organic compounds (VOX) inside the coop.


## License

This project is licensed under the MIT License - see the [LICENSE](https://raw.githubusercontent.com/Tom-Camp/fe/refs/heads/main/LICENSE)
file for details.
