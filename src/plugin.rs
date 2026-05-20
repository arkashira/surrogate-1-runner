use kicad_plugin::Plugin;
use kicad_plugin::PluginRegistrar;

/// The Axentx plugin struct.
struct AxentxPlugin;

impl Plugin for AxentxPlugin {
    /// Returns the name of the plugin.
    fn name(&self) -> &str {
        "Axentx Plugin"
    }

    /// Called when the plugin is activated from the menu.
    fn on_menu(&self) {
        // TO DO: implement plugin functionality, such as:
        // - Creating a new menu item
        // - Handling user input
        // - Interacting with the KiCAD API
    }
}

#[no_mangle]
pub extern "C" fn plugin_register(reg: &mut PluginRegistrar) {
    // Register the plugin with KiCAD.
    reg.register_plugin(Box::new(AxentxPlugin));
}