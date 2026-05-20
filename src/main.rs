use kicad_plugin::action_plugin::ActionPlugin;
use kicad_plugin::pcbnew::PcbnewPlugin;

fn main() {
    let plugin = PcbnewPlugin::new();
    plugin.register_action("axentx_surrogate_1", |frame| {
        frame.show_info_bar_msg("axentx surrogate 1 plugin loaded");
    });
    plugin.run();
}