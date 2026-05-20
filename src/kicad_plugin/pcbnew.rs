// Implementation of PcbnewPlugin
use crate::action_plugin::{ActionPlugin, PcbnewActionPlugin};

pub struct PcbnewPlugin {
    inner: PcbnewActionPlugin,
}

impl PcbnewPlugin {
    pub fn new() -> Self {
        Self {
            inner: PcbnewActionPlugin::new(),
        }
    }

    pub fn register_action(&self, name: &str, action: impl Fn(&mut dyn PcbnewFrame) + 'static) {
        self.inner.register_action(name, action);
    }

    pub fn run(&self) {
        self.inner.run();
    }
}