#show running application listΩ
yarn application --list

yarn application -appStates RUNNING -list | grep "applicationName"

#kill running app
yarn application -kill application_16292842912342_34127
