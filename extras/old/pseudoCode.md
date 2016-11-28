#PsedoCode:

## connect to listener
  initialize stepper_rotation_count

def main() function:
  ## read ldr_reading()
    conn.send(ldr_reading)
    if ldr_reading>threshold
        conn.send('patch_found')
        stop
    else:
        if Distance_sensor< threshold_distance:
            conn.send('turning 90')
            turn_left()
            update stepper_rotation_count
            conn.send('moving forward x')
            update stepper_rotation_count
            conn.send('turning 90')
            turn_left()
            update stepper_rotation_count
            conn.send('moving forward')
            move_forward()
            main() #recursion
            update stepper_rotation_count
main()
