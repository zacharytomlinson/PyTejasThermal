#!/bin/bash

cd ~
sed -i -- 's/autohide=0/autohide=1/g' ~/.config/lxpanel/LXDE-pi/panels/panel
sed -i -- 's/heightwhenhidden=2/heightwhenhidden=0/g' ~/.config/lxpanel/LXDE-pi/panels/panel