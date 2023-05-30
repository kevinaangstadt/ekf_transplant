from pymavlink import mavextra, mavutil, mavwp

def generate_circle(lat, lon, initial_bearing, radius, num_points):
    """
    Generate a mission with waypoints radius distance from the latitude and
    longitude provided
    """

    points = []

    angle = 360 // num_points

    for i in range(num_points):
        bearing = mavextra.wrap_360(i * angle + initial_bearing)

        points.append(mavextra.gps_newpos(lat, lon, bearing, radius))
    
    return points

def generate_mission(lat, lon, bearing, radius, num_points=6, error=1):
    mission = mavwp.MAVWPLoader()

    # add the initial as home
    mission.add_latlonalt(lat, lon, 0)

    for (lat, lon) in generate_circle(lat, lon, bearing, radius, num_points):
        mission.add(mavutil.mavlink.MAVLink_mission_item_message(
            mission.target_system,
            mission.target_component,
            0, # sequence gets overwritten
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
            0, 0, 0, error, 0, 0,
            lat, lon, 0
        ))
        #mission.add_latlonalt(lat, lon, 0)
    
    mission.add(mavutil.mavlink.MAVLink_mission_item_message(
        mission.target_system,
        mission.target_component,
        0, # sequence gets overwritten
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
        mavutil.mavlink.MAV_CMD_DO_JUMP,
        0, 0, 1, -1, 0, 0,
        lat, lon, 0
    ))

    return mission
