

def switch_to_new_window(driver):
    current_handle = driver.current_window_handle
    window_handles = driver.window_handles
    for handle in window_handles:
        if handle != current_handle:
            driver.switch_to.window(handle)
    return driver.current_url
