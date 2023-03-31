#!/usr/bin/env python3


import asyncio
import time
import math
from mavsdk import System
from mavsdk.offboard import (OffboardError, VelocityBodyYawspeed, VelocityNedYaw)
import pid
import pickle
async def run():
    
    
    drone = System()
    #await drone.connect(system_address="udp://:14540")
    await drone.connect(system_address="serial:///dev/ttyACM0:57600")
    print("bağlantı bekleniyor")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"drone Bulundu....")
            break

    print("-- Arm Oluyor..")
    await drone.action.arm()
    print("-- Kalkıyor....")
    await drone.action.takeoff()
    await asyncio.sleep(5)
    time.sleep(5)

    print("-- Başlangıç Boktası Ayarlandı..") #baslangıç açısı değistirilecek
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))

    print("-- Offboard Mode Başlatıldı")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Offboar mode baslatılması : \
              {error._result.result} nedeniyle hata verdi.. ")
        print("-- Motorlar Duruyor..")
        await drone.action.disarm()
        return

    #####---Araç Takip Kodu-----#####


    while True:
        try:
            with open("pay1.pkl", "rb") as f:
                koordinat = pickle.load(f)
                #time.sleep(3)
        except (EOFError):
            pass
            print("okuma hatasi")

        a_e = koordinat[0]
        a_n = koordinat[1]
        hiz = pid.pidss(a_e,a_n)
        veri0 = math.fabs(hiz[0])
        veri1 = math.fabs(hiz[1])
        #640 yatay genişlik, 360 dikey uzunuk değerleri
        #print("veri0:",veri0)
        #print("veri1:",veri1)
        if (cx > 300 and cx < 340 and cy > 220 and cy < 260):
            #print("Merkezde")
            await drone.offboard.set_velocity_ned(VelocityNedYaw(cx, cy, 0.0, 0.0))
            await asyncio.sleep(0.30)
        
        if cx<300:
            if cy<260:
                #print("hedef ekranın sol üstünde")
                await drone.offboard.set_velocity_ned(VelocityNedYaw(cx, -cy, 0.0, 0.0))
                await asyncio.sleep(0.30)

            else:
                #print("hedef ekranın sol altında")
                await drone.offboard.set_velocity_ned(VelocityNedYaw(-cx, -cy, 0.0, 0.0))
                await asyncio.sleep(0.30)

        if cx>340:
            if cy<220:
                #print("hedef ekranın sağ üstünde")
                await drone.offboard.set_velocity_ned(VelocityNedYaw(cx, cy, 0.0, 0.0))
                await asyncio.sleep(0.30)

            else:
                #print("hedef ekranın sağ altında")
                await drone.offboard.set_velocity_ned(VelocityNedYaw(-cx, cy, 0.0, 0.0))
                await asyncio.sleep(0.30)

        
    

    
    

    print("Görevler Tamamlandı, drone İniyor..")
    print("-- 1 sn Bekle")
    await drone.offboard.set_velocity_body(
        VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
    await asyncio.sleep(1)

    print("-- Offboar Mode Durdu")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Offboar mode baslatılması : \
              {error._result.result} nedeniyle hata verdi..")
    print("-- Landing")
    await drone.action.land()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    
