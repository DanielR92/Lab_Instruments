import ETMXXXXP

test = ETMXXXXP.ETMXXXXP("COM18", debug=True)

test.connect()

test.setVoltage(10)
test.setCurrentLimit(1)
test.setOutput(True)
test.setOutput(False)

limit = test.getCurrentLimit()
test.setCurrentLimit(limit * 2)


test.setOutput(True)
test.setOutput(False)

if(test.getOutputStats()):
    print("Output is on")
else:
    print("Output is off")
    test.setBuzzer(True)
    test.setVoltage(20)


