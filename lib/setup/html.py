import strings as s
from Configuration import config


def get_html_form():
    """
    Constructs a webpage that includes a form to fill in by the user to acquire new configurations for the device
    :return: html_form
    :rtype: str
    """

    if config.get_config("LORA") == "ON":
        lora_check = " checked"
    else:
        lora_check = ""

    selected_region = {"Europe": "", "Asia": "", "Australia": "", "United States": ""}
    for option in selected_region:
        if option == config.get_config("region"):
            selected_region[option] = " selected"

    selected_TEMP = {"SHT35": "", "OFF": ""}
    for option in selected_TEMP:
        if option == config.get_config(s.TEMP):
            selected_TEMP[option] = " selected"

    selected_PM1 = {"PMS5003": "", "SPS030": "", "OFF": ""}
    for option in selected_PM1:
        if option == config.get_config(s.PM1):
            selected_PM1[option] = " selected"

    selected_PM2 = {"PMS5003": "", "SPS030": "", "OFF": ""}
    for option in selected_PM2:
        if option == config.get_config(s.PM2):
            selected_PM2[option] = " selected"

    selected_GPS = {"SIM28": "", "OFF": ""}
    for option in selected_GPS:
        if option == config.get_config("GPS"):
            selected_GPS[option] = " selected"

    selected_logging = {"Critical": "", "Error": "", "Warning": "", "Info": "", "Debug": ""}
    for level in selected_logging:
        if level == config.get_config("logging_lvl"):
            selected_logging[level] = " selected"

    with open("form.html", "r") as html_file:
        html = html_file.read()

    # This is kinda cumbersome but allows for easy insertion into the html.
    return html.format(
        unique_id = str(config.get_config("device_id")),
        device_name = str(config.get_config("device_name")),
        password = str(config.get_config("password")),
        config_timeout = str(config.get_config("config_timeout")),
        device_eui = str(config.get_config("device_eui")),
        application_eui = str(config.get_config("application_eui")),
        app_key = str(config.get_config("app_key")),
        fair_access = str(config.get_config("fair_access")),
        air_time = str(config.get_config("air_time")),
        SSID = str(config.get_config("SSID")),
        wifi_password = str(config.get_config("wifi_password")),
        TEMP_id = str(config.get_config("TEMP_id")),
        TEMP_period = str(config.get_config("TEMP_period")),
        PM1_id = str(config.get_config("PM1_id")),
        PM1_init = str(config.get_config("PM1_init")),
        interval = str(config.get_config("interval")),
        PM2_id = str(config.get_config("PM2_id")),
        PM2_init = str(config.get_config("PM2_init")),
        GPS_id = str(config.get_config("GPS_id")),
        GPS_timeout = str(config.get_config("GPS_timeout")),
        GPS_period = str(config.get_config("GPS_period")),
        lora_check = lora_check,
        eu_selected = str(selected_region["Europe"]),
        as_selected = str(selected_region["Asia"]),
        au_selected = str(selected_region["Australia"]),
        us_selected = str(selected_region["United States"]),
        temp_selected_SHT35 = str(selected_TEMP["SHT35"]),
        temp_selected_off = str(selected_TEMP["OFF"]),
        PM1_PMS5003_selected = str(selected_PM1["PMS5003"]),
        PM1_SPS030_selected = str(selected_PM1["SPS030"]),
        PM1_selected_off = str(selected_PM1["OFF"]),
        PM2_PMS5003_selected = str(selected_PM2["PMS5003"]),
        PM2_SPS030_selected = str(selected_PM2["SPS030"]),
        PM2_selected_off = str(selected_PM2["OFF"]),
        gps_selected_SIM28 = str(selected_GPS["SIM28"]),
        gps_selected_off = str(selected_GPS["OFF"]),
        logging_level_selected_critical = str(selected_logging["Critical"]),
        logging_level_selected_error = str(selected_logging["Error"]),
        logging_level_selected_warning = str(selected_logging["Warning"]),
        logging_level_selected_info = str(selected_logging["Info"]),
        logging_level_selected_debug = str(selected_logging["Debug"]),
    )
