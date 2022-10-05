import signal
from xbox360controller import Xbox360Controller

# axis_l JOYSTICK SINISTRO
# axis_r JOYSTICK DESTRO
# hat FRECCE
# trigger_l LT
# trigger_r RT
# button_a A
# button_b B
# button_x X
# button_y Y
# button_trigger_l LB
# button_trigger_r RB
# button_select SELECT
# button_start START
# button_mode MENU
# button_thumb_l JOYSTICK SINISTRO
# button_thumb_r JOYSTICK DESTRO

def on_button_pressed(button):
    print('Button {0} was pressed'.format(button.name))

def on_button_released(button):
    print('Button {0} was released'.format(button.name))

def on_axis_moved(axis):
    print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))

def on_trigger_pressed(button):
    print('Button {0} was pressed to {1}'.format(button.name, button.value))

try:
    with Xbox360Controller(0, axis_threshold=0.2) as controller:
        controller.info()

        # Button A events
        controller.button_a.when_pressed = on_button_pressed
        controller.button_a.when_released = on_button_released

        # Button B events
        controller.button_b.when_pressed = on_button_pressed
        controller.button_b.when_released = on_button_released

        # Button Y events
        controller.button_y.when_pressed = on_button_pressed
        controller.button_y.when_released = on_button_released

        # Button X events
        controller.button_x.when_pressed = on_button_pressed
        controller.button_x.when_released = on_button_released

        # Button Start and Select events
        controller.button_start.when_pressed = on_button_pressed
        controller.button_start.when_released = on_button_released

        controller.button_select.when_pressed = on_button_pressed
        controller.button_select.when_released = on_button_released

        # Button Mode events
        controller.button_mode.when_pressed = on_button_pressed
        controller.button_mode.when_released = on_button_released

	    # Button Trigger events
        controller.button_trigger_l.when_pressed = on_button_pressed
        controller.button_trigger_l.when_released = on_button_released

        controller.button_trigger_r.when_pressed = on_button_pressed
        controller.button_trigger_r.when_released = on_button_released

        controller.trigger_l.when_moved = on_trigger_pressed
        controller.trigger_r.when_moved = on_trigger_pressed

        # Hat buttons events
        controller.hat.when_moved = on_axis_moved

        # Left and right axis move and press event
        controller.axis_l.when_moved = on_axis_moved
        controller.axis_r.when_moved = on_axis_moved

        controller.button_thumb_l.when_pressed = on_button_pressed
        controller.button_thumb_l.when_released = on_button_released

        controller.button_thumb_r.when_pressed = on_button_pressed
        controller.button_thumb_r.when_released = on_button_released

        signal.pause()
except KeyboardInterrupt:
    pass
