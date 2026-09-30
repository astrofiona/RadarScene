import numpy as np
import matplotlib.pyplot as plt

# Import required HermesPy modules
from hermespy.channel import SingleTargetRadarChannel
from hermespy.simulation import SimulatedDevice
from hermespy.jcas import OFDMRadar, MatchedFilterJcas
from hermespy.modem import OTFSWaveform,GridResource,PrefixType,OFDMWaveform,GridElement,ElementType,SymbolSection
from hermespy.radar import MaxDetector, Radar, FMCW, ThresholdDetector
np.random.seed = 21006192


i = input('Which radar scenario? 1: FMCW, 2: OFDM, 3: OTFS \n')
if (int(i) == 1):
    device = SimulatedDevice(
        carrier_frequency=24e9,
        bandwidth=1024*90.909e3,
        oversampling_factor=4,
    )
    
    radar = Radar()
    radar.waveform = FMCW(num_chirps=3, chirp_duration=1e-6, pulse_rep_interval=1.1e-6)
    device.add_dsp(radar)
    rngPerc = 0.01*np.random.randint(1,99);
    # Create a new radar channel with a single illuminated target
    target = SingleTargetRadarChannel(rngPerc * radar.max_range(device.bandwidth), 1., attenuate=True)

    transmission = device.transmit()
    device.transmit().mixed_signal.plot(title='Single Radar Chirp').show()
    propagation = target.propagate(transmission, device, device)
    reception = device.receive(propagation)
    reception.operator_receptions[0].cube.plot_range()
    plt.show()

    print('Target Range: ' + str(rngPerc*radar.max_range(device.bandwidth)) + ' m')
elif (int(i) == 2):
    device = SimulatedDevice(
        carrier_frequency=24e9,
        bandwidth=128*90.909e3,
        oversampling_factor=4,
    )
    waveform = OFDMWaveform(
        grid_resources=[
            GridResource(16, PrefixType.CYCLIC, .1, [GridElement(ElementType.DATA, 7), GridElement(ElementType.REFERENCE, 1)]),
            GridResource(16, PrefixType.CYCLIC, .1, [GridElement(ElementType.DATA, 1)]),
        ],
        grid_structure=[
            SymbolSection(64, [0, 1])
        ],
        num_subcarriers=128,
    )
    radar = MatchedFilterJcas(waveform = waveform, max_range=1650, max_velocity = 500)
    radar.detector=ThresholdDetector(.95, peak_detection=False)
    device.add_dsp(radar)
    rngPerc = 0.01*np.random.randint(10,90);
    # Generate a single illuminated target
    radar_channel = SingleTargetRadarChannel(rngPerc * radar.max_range, 1., velocity=161, attenuate=True)
    device.transmit().mixed_signal.plot(title='Single Radar Chirp').show()
    transmission = device.transmit()
    propagation = radar_channel.propagate(transmission, device, device)
    reception = device.receive(propagation)
    
    reception.operator_receptions[0].cube.plot_range()
    plt.show()
    print('Target Range: ' + str(rngPerc*radar.max_range) + ' m')
    
elif (int(i)==3):
    device = SimulatedDevice(
        carrier_frequency=24e9,
        bandwidth=128*90.909e3,
        oversampling_factor=4,
    )
    waveform = OTFSWaveform(
        grid_resources=[
            GridResource(16, PrefixType.CYCLIC, .1, [GridElement(ElementType.DATA, 7), GridElement(ElementType.REFERENCE, 1)]),
            GridResource(16, PrefixType.CYCLIC, .1, [GridElement(ElementType.DATA, 1)]),
            ],
        grid_structure = [
           SymbolSection(64, [0,1])
           ],
        num_subcarriers=128,
    )
    radar = MatchedFilterJcas(
        max_range=1650,
        waveform=waveform,
        max_velocity=500,
        
        )
    radar.detector=ThresholdDetector(.95, peak_detection=False)
    device.add_dsp(radar)
    rngPerc = 0.01*np.random.randint(10,90);
    # Create a new radar channel with a single illuminated target
    target = SingleTargetRadarChannel(rngPerc*radar.max_range, 1., velocity=20, attenuate=True)
    device.transmit().mixed_signal.plot(title='Single Radar Chirp').show()
    transmission = device.transmit()
    propagation = target.propagate(transmission, device, device)
    reception = device.receive(propagation)
    reception.operator_receptions[0].cube.plot_range()
    plt.show()
    print('Target Range: ' + str(rngPerc*radar.max_range) + ' m')
    



