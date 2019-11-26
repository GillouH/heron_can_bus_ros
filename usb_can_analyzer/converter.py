#!/usr/bin/env python3
# coding: utf-8


from typing import Union, Tuple

from serial import Serial

from usb_can_analyzer.useful import getNbByte


# Certaines méthodes prédéfinies en standard messages -> Changer en choix entre standard et extended
# Traiter les vérifications d'erreur
class Converter:
    # ID MSG
    STANDARD, EXTENDED = (0, 1)	# ID MSG type
    ID_MSG_TYPE_SIZE = {		# ID MSG size in byte
        STANDARD: 2,
        EXTENDED: 4
    }
    # TYPE FRAME
    DATA, REMOTE = (0, 1)
    TYPE_MSG = (DATA, REMOTE)

    FIRST_BYTE = b'\xaa'	# Constant use for the USB protocol with the converter USB/CAN.
    LAST_BYTE = b'\x55'		# Constant use for the USB protocol with the converter USB/CAN.

    def __init__(self, port: str = "/dev/ttyUSB0", baudrate: int = 1228800, idMsgType: int = STANDARD):
        if idMsgType not in Converter.ID_MSG_TYPE_SIZE.keys():	# We check that the idMsgType is a suitable value.
            raise ValueError("Not a valid idMsgSize: " + str(idMsgType))
        self.idMsgType = idMsgType
        self.comUSB = Serial(port, baudrate, timeout=0)

    # WRITING PART
    def sendMessage(self, msgType: int, serviceID: int, nodeID: int, payload: str) -> None:
        msgID = self.createMsgID(serviceID, nodeID)
        frame = (
            self.FIRST_BYTE
            + self.createConfigByte(msgID, payload, msgType)
            + msgID
            + self.createPayload(payload)
            + self.LAST_BYTE
        )
        self.comUSB.write(frame)

    def createConfigByte(self, idMsg: Union[int, str, bytes], payload: Union[int, str, bytes], typeFrame: int = DATA) -> bytes:
        idMsgNbByte = getNbByte(idMsg)					# We check that the number of bytes for the msg ID is not too large.
        if idMsgNbByte > Converter.ID_MSG_TYPE_SIZE[self.idMsgType]:
            raise ValueError("idMsg too large: " + str(idMsg))
        payloadNbByte = getNbByte(payload)	# We check that payload is not too to large.
        if payloadNbByte > 0b1111:
            raise ValueError("payload too large. It must contain at the most " + str(0b1111) + " bytes. payload: " + str(payload) + ", nb bytes: " + str(payloadNbByte))
        if typeFrame not in Converter.TYPE_MSG:		# We check that typeFrame is either DATA or REMOTE.
            raise ValueError("Not a valid type frame: " + str(typeFrame))

        configByte  = 0b11000000												# We set the 2 first bits to 1 for the converter USB/CAN.
        configByte += 0b00100000 if self.idMsgType == Converter.EXTENDED else 0	# If necessary, we change the bit associated with the number of byte in the msg id.
        configByte += 0b00010000 if typeFrame == Converter.REMOTE else 0		# If necessary, we change the bit associated with the msg type (REMOTE ou DATA).
        configByte += getNbByte(payload)										# We add the number of bytes for the payload
        return bytes.fromhex(format(configByte, "02x"))

    def createMsgID(self, serviceID: int, nodeID: int) -> bytes:
        if serviceID > 0b11111:		# We check that serviceID is not too large.
            raise ValueError("serviceID is too large: " + str(serviceID))
        if nodeID > 0b111111:		# We check that nodeID is not too large.
            raise ValueError("nodeId is too large: " + str(nodeID))
        # The msg ID contains the nodeID on his 6 less signiicant bits, and the service ID on his next 5.
        msgID = (serviceID << 6) + nodeID	# In binary, we add the nodeID in the less significant bit
        msgID = format(msgID, "04x")
        return bytes.fromhex(msgID)[::-1]

    def createPayload(self, data: str) -> bytes:
        if len(data) > 0b1111*2:
            raise ValueError("Too many hexadecimal digits.")
        if len(data) % 2 == 1:
            data = "0" + data
        return bytes.fromhex(data)

    # READING PART
    def readMessage(self) -> Tuple[int, int, int, str]:
        if (self.comUSB.read() != self.FIRST_BYTE): return -1
        msgType, lengthID, lengthPayload = self.getConfigByte()
        serviceID, nodeID = self.getMsgID(lengthID)
        msgPayload = self.getMsgPayload(lengthPayload)
        if(self.comUSB.read() != self.LAST_BYTE): return -1
        return msgType, serviceID, nodeID, msgPayload

    def getConfigByte(self) -> Tuple[int, int, int]:
        configByte = int(self.comUSB.read().hex(), base=16)
        msgType = Converter.TYPE_MSG[int(format(configByte, 'b')[3])]
        lengthID = Converter.ID_MSG_TYPE_SIZE[int(format(configByte, 'b')[2])]
        lengthPayload = int(format(configByte, "x")[1], base=16)
        return msgType, lengthID, lengthPayload

    def getMsgID(self, lengthID: int) -> Tuple[int, int]:
        msgID = bytes()
        for i in range(lengthID): msgID += self.comUSB.read()
        msgID = int(msgID[::-1].hex(), base=16)
        serviceID = msgID >> 6
        nodeID = msgID - (serviceID << 6)
        return serviceID, nodeID

    def getMsgPayload(self, lengthPayload: int) -> str:
        msgPayload = ""
        for i in range(lengthPayload): msgPayload += self.comUSB.read().hex()
        return msgPayload

    def __del__(self):
        del self.comUSB


if __name__ == "__main__":
    try:
        converter = Converter("/dev/ttyUSB0")
        while True:
            converter.sendMessage(Converter.DATA, 0b1010, 0b111010, input())
            #data = converter.readMessage()
            #if type(data) != int:
                #print(data)
    except KeyboardInterrupt:
        pass
    finally:
        pass
