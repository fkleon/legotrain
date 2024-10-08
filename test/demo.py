import logging
import statistics as stat
import time
from colorsys import rgb_to_hsv
from time import sleep

from pylgbst.hub import SmartHub
from pylgbst.peripherals import (
    COLOR_BLACK,
    COLOR_GREEN,
    COLORS,
    Current,
    Voltage,
)

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("hub")


def demo_voltage(hub):

    def callback1(value):
        print("Amperage: %s", value)

    def callback2(value):
        print("Voltage: %s", value)

    print(dir(hub.current))

    hub.current.subscribe(callback1, mode=Current.CURRENT_L, granularity=0)
    hub.current.subscribe(callback1, mode=Current.CURRENT_L, granularity=1)

    hub.voltage.subscribe(callback2, mode=Voltage.VOLTAGE_L, granularity=0)
    hub.voltage.subscribe(callback2, mode=Voltage.VOLTAGE_L, granularity=1)
    time.sleep(5)
    hub.current.unsubscribe(callback1)
    hub.voltage.unsubscribe(callback2)

def demo_led_colors(hub):
    # LED colors demo
    print("LED colors demo")

    # We get a response with payload and port, not x and y here...
    def colour_callback(named):
        print("LED Color callback: %s", named)

    hub.led.subscribe(colour_callback)
    for color in list(COLORS.keys())[1:] + [COLOR_BLACK, COLOR_GREEN]:
        print("Setting LED color to: %s", COLORS[color])
        hub.led.set_color(color)
        sleep(1)

def demo_motor(hub):
    print("Train motor movement demo (on port A)")

    motor = hub.port_A
    print(motor)

    motor.power_index()
    sleep(3)
    motor.stop()
    sleep(1)
    motor.power_index(param=0.2)
    sleep(3)
    motor.stop()
    sleep(1)
    motor.power_index(param=-0.2)
    sleep(3)
    motor.stop()
    sleep(3)

def demo_color_sensor(smart_hub):
    print("Color sensor test: wave your hand in front of it")
    demo_color_sensor.cnt = 0
    limit = 300

    bg_list = []
    gr_list = []
    h_list = []
    s_list = []
    v_list = []

    def callback(*args, **kwargs):
        demo_color_sensor.cnt += 1

        # use HSV as criterion for mapping colors
        r = args[0]
        g = args[1]
        b = args[2]

        h, s, v = rgb_to_hsv(r, g, b)

        if h >= 1. or h <= 0.:
            return

        if max(r, g, b) > 10.0 and v > 20.0:
            h_list.append(h)
            s_list.append(s)
            v_list.append(v)

            bg = b / g
            gr = g / r

            bg_list.append(bg)
            gr_list.append(gr)

            red_detection = "other"
            if (h > 0.90 or h < 0.05) and (s > 0.55 and s < 0.80):
                red_detection = "RED"
            elif (h > 0.55 and h < 0.62) and (s > 0.50 and s < 0.72):
                red_detection = "LIGHT BLUE"
            elif (h > 0.15 and h < 0.30) and (s > 0.23 and s < 0.55):
                red_detection = "LIGHT GREEN"
            elif (h > 0.40 and h < 0.60) and (s > 0.25 and s < 0.60):
                red_detection = "GREEN"
            elif (h > 0.58 and h < 0.78) and (s > 0.19 and s < 0.40):
                red_detection = "DARK GRAY (track)"


            print(demo_color_sensor.cnt, limit, args, kwargs, h, s, v, bg, gr, red_detection)

    smart_hub.vision_sensor.subscribe(callback, granularity=3, mode=6)

    while demo_color_sensor.cnt < limit:
        time.sleep(1)

    smart_hub.vision_sensor.unsubscribe(callback)

    print("H stats: ", stat.mean(h_list), stat.stdev(h_list), min(h_list), max(h_list))
    print("S stats: ", stat.mean(s_list), stat.stdev(s_list), min(s_list), max(s_list))
    print("V stats: ", stat.mean(v_list), stat.stdev(v_list), min(v_list), max(v_list))
    print("BG stats: ", stat.mean(bg_list), stat.stdev(bg_list), min(bg_list), max(bg_list))
    print("GR stats: ", stat.mean(gr_list), stat.stdev(gr_list), min(gr_list), max(gr_list))

    # TODO fix this by disambiguing circularity
    # each row lists mean, stddev, min, max.

# red tile
# H stats:  0.9621906972631104 0.006721242377437976 0.9444444444444444 0.9838709677419355
# S stats:  0.7093463686371333 0.025478670186998724 0.6341463414634146 0.8048780487804879
# V stats:  40.93790849673203 1.404699677882188 38.0 45.0
# BG stats:  1.5667745380980675 0.1506054037896563 1.2 2.375
# GR stats:  0.29065363136286665 0.02547867018699872 0.1951219512195122 0.36585365853658536

# yellow train body
# H stats:  0.9699768656786121 0.007091169148411911 0.9506172839506173 0.9833333333333334
# S stats:  0.5789389809847681 0.016827702533681536 0.5306122448979592 0.6122448979591837
# V stats:  48.943396226415096 1.4483550247921277 45.0 52.0
# BG stats:  1.2489999780693188 0.0631834493177173 1.1304347826086956 1.4
# GR stats:  0.4210610190152318 0.016827702533681543 0.3877551020408163 0.46938775510204084

# red circle
# H stats:  0.8898214661558889 0.15234378462194229 0.016666666666666663 0.9861111111111112
# S stats:  0.465337099050416 0.06508904935304234 0.3333333333333333 0.6190476190476191
# V stats:  24.962962962962962 2.4109283203910765 21.0 30.0
# BG stats:  1.4699570105820106 0.28472005791778354 0.9285714285714286 2.090909090909091
# GR stats:  0.5358646396966126 0.06666976078669581 0.38095238095238093 0.7142857142857143

# orange - seems indistibguishable from red
# H stats:  0.7436221049328164 0.42800810737238887 0.0037878787878787845 0.9972677595628415
# S stats:  0.8156968777816735 0.05295759376080173 0.68 0.90625
# V stats:  45.12337662337662 17.909477507798094 21.0 91.0
# BG stats:  1.1511557352388542 0.24885596264304252 0.6875 2.0
# GR stats:  0.19708319599959584 0.06990274040261603 0.09375 0.4

    # dark blue tile (not to be used)
    # H stats:  0.657232420420557 0.05940983030915233 0.5490196078431372 0.9320987654320988
    # S stats:  0.4502750567049586 0.10337623196677968 0.09090909090909091 0.6842105263157895
    # V stats:  34.99261992619926 6.903564629381398 21.0 59.0

    # yellow train body - values spread around origin
    # H stats:  0.9894320853790294 0.003909771634062216 0.9810126582278481 0.9981684981684982
    # S stats:  0.6331090625363353 0.013603490642704025 0.6063829787234043 0.6694915254237288
    # V stats:  165.92409240924093 59.60274822893457 90.0 292.0

    # H stats:  0.9658811813734542 0.05679645486571017 0.008771929824561412 0.9933333333333333
    # S stats:  0.565825953105329 0.022356157299963583 0.5 0.6304347826086957
    # V stats:  43.325581395348834 4.345147877520325 33.0 50.0
    # BG stats:  1.2439604392659092 0.1064035262424097 0.9473684210526315 1.5294117647058822
    # GR stats:  0.4342638376821362 0.022619686382698442 0.3695652173913043 0.5135135135135135


    # carpet- values spread around origin
    # H stats:  0.05236174877835684 0.05367047447782348 0.012820512820512811 0.9523809523809523
    # S stats:  0.3151364968520766 0.027335502239051256 0.23333333333333334 0.3888888888888889
    # V stats:  72.24422442244224 24.728052506630195 24.0 170.0

    # white tile
    # H stats:  0.7637420853168304 0.022818653223407467 0.7083333333333334 0.8333333333333334
    # S stats:  0.15673942718972475 0.04220747621377944 0.05555555555555555 0.2546583850931677
    # V stats:  217.53246753246754 23.024747720056183 159.0 283.0

    # gray track
    # H stats:  0.6240816726904218 0.048370112846115546 0.4583333333333333 0.7424242424242425
    # S stats:  0.23150187264977184 0.04753992183667234 0.08235294117647059 0.38333333333333336
    # V stats:  68.44408945686901 9.540949457788486 43.0 97.0

    # dark gray tile
    # H stats:  0.3815025234909023 0.015834242652109597 0.3466666666666667 0.4479166666666667
    # S stats:  0.6323943138609877 0.06786865621567133 0.4375 0.9166666666666666
    # V stats:  64.91570881226053 23.952689394036554 21.0 107.0

# medium blue
# H stats:  0.6355270124053662 0.008371171049406817 0.6111111111111112 0.6822916666666666
# S stats:  0.7714094492782996 0.07327748358345455 0.4888888888888889 0.8679245283018868
# V stats:  78.70431893687707 19.341896182930814 21.0 125.0
# BG stats:  2.7237578049746873 0.35426986846525443 1.6511627906976745 3.5
# GR stats:  1.716136243338517 0.30799059033022896 0.8928571428571429 2.857142857142857



DEMO_CHOICES = {
    # 'all': demo_all,
    'voltage': demo_voltage,
    'led_colors': demo_led_colors,
    'color_sensor': demo_color_sensor,
    'motor': demo_motor
}

hub_1 = SmartHub(address='86996732-BF5A-433D-AACE-5611D4C6271D')   # test hub
# hub_2 = SmartHub(address='F88800F6-F39B-4FD2-AFAA-DD93DA2945A6')   # train hub

# device_1 = HandsetRemote(address='2BC6E69B-5F56-4716-AD8C-7B4D5CBC7BF8')  # test handset
# device_1 = HandsetRemote(address='5D319849-7D59-4EBB-A561-0C37C5EF8DCD')  # train handset

# for device in device_1.peripherals:
#     print("device:   ", device)

try:
    # demo = DEMO_CHOICES['motor']
    # demo(hub_1)
    # demo(hub_2)

    # demo = DEMO_CHOICES['led_colors']
    # demo(hub_1)
    # demo(hub_2)

    # demo = DEMO_CHOICES['voltage']
    # demo(hub_1)
    # demo(hub_2)

    demo = DEMO_CHOICES['color_sensor']
    demo(hub_1)
    # demo(hub_2)

finally:
    pass
    hub_1.disconnect()
    # hub_2.disconnect()
    # device_1.disconnect()
