import matplotlib.pyplot as plt
from bitstring import BitArray
import serial
import os
import time


def run(port, speed, dirName, num=1, message=b'\01', saving=True, uGraph=True, iGraph=False):
    ser = serial.Serial(port=port,
                        baudrate=speed,
                        # stopBits=selectedStopBits
                        )  # open serial port

    print(ser.getSettingsDict())
    ser.isOpen()

    ser.write(message)
    data = ""

    while True:
        response = ser.read_all()

        if len(response) != 0:
            data += str(response)
            print(response)
            if "x07" in str(response):
                # print("end")
                break

    ser.close()

    listData = data.split("\\x")

    u0 = []
    i0 = []

    scale = 16  ## equals to hexadecimal
    num_of_bits = 8
    numOfLines = 1
    nums = []

    for i in listData:
        i = i.replace("'b'", "")
        try:
            if len(i) == 2:
                nums.append(bin(int(i, scale))[2:].zfill(num_of_bits))
            if len(i) == 3:
                nums.append((bin(ord(i[-1]))[2:].zfill(num_of_bits)))

        except:
            # print("error" + i)
            pass


    for i in nums:
        print(i)

    for i in range(len(nums)):
        if str(nums[i])[:4] == "0100":
            i0.append(
                str(nums[i])[4:] + str(nums[i + 1]) + str(nums[i + 2]) + str(nums[i + 3]) + str(nums[i + 4]))
        elif str(nums[i])[:4] == "0110":
            u0.append(
                str(nums[i])[4:] + str(nums[i + 1]) + str(nums[i + 2]) + str(nums[i + 3]) + str(nums[i + 4]))

    U = []
    I = []
    u1 = []

    for i in range(len(u0)):
        u0bin = (str(u0[i])[0] + str(u0[i])[5:12] + str(u0[i])[1] + str(u0[i])[13:20] + str(u0[i])[2] + str(
            u0[i])[
                                                                                                        21:28] +
                 str(u0[i])[3] + str(u0[i])[29:36])
        U.append((BitArray(bin=u0bin).int))
        u1.append(u0bin)

    for i in range(len(i0)):
        i0bin = (str(i0[i])[0] + str(i0[i])[5:12] + str(i0[i])[1] + str(i0[i])[13:20] + str(i0[i])[2] + str(
            i0[i])[
                                                                                                        21:28] +
                 str(i0[i])[3] + str(i0[i])[29:36])
        I.append((BitArray(bin=i0bin).int))



    if saving:
        try:
            os.mkdir(dirName)
        except:
            pass
        saveData(dirName, num, U, I)

    if uGraph:
        plt.figure(1)
        plt.plot(range(len(U)), U)
        plt.show()

    if iGraph:
        plt.figure(2)
        plt.plot(range(len(I)), I)
        plt.show()


def calibration(port,speed):
    run(port, speed, "calibration", message=b'\xFF', saving=False, uGraph=False, iGraph=True)



def saveData(dirName, num, U, I):
    print("U = ", U)
    print("I = ", I)


    for i in range(len(U)):
        fileName = dirName + "/%s.txt" % num
        with open(fileName, "a") as file:
            file.write(str(I[i]) + " " + str(U[i]))
            file.write("\n")


