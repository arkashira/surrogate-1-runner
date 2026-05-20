// Implementation of ActionPlugin trait and related functionality
pub trait ActionPlugin {
    fn register_action(&self, name: &str, action: impl Fn(&mut dyn PcbnewFrame) + 'static);
    fn run(&self);
}

pub struct PcbnewActionPlugin {
    // internal state
}

impl PcbnewActionPlugin {
    pub fn new() -> Self {
        Self {
            // initialize internal state
        }
    }
}

impl ActionPlugin for PcbnewActionPlugin {
    fn register_action(&self, name: &str, action: impl Fn(&mut dyn PcbnewFrame) + 'static) {
        // implementation to register action with KiCAD
    }

    fn run(&self) {
        // implementation to run the plugin
    }
}

// PcbnewFrame trait definition
pub trait PcbnewFrame {
    fn show_info_bar_msg(&mut self, msg: &str);
}