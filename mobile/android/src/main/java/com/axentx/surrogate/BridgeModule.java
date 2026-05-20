package com.axentx.surrogate;

import com.axentx.surrogate.model.SurrogateModel;
import com.axentx.surrogate.model.SurrogateOptions;
import com.axentx.surrogate.model.SurrogatePrompt;

import java.util.HashMap;
import java.util.Map;

import io.flutter.embedding.engine.plugins.FlutterPlugin;
import io.flutter.plugin.common.MethodCall;
import io.flutter.plugin.common.MethodChannel;
import io.flutter.plugin.common.MethodChannel.MethodCallHandler;
import io.flutter.plugin.common.MethodChannel.Result;

public class BridgeModule implements FlutterPlugin, MethodCallHandler {
    private static final String CHANNEL = "com.axentx/surrogate";
    private MethodChannel channel;

    @Override
    public void onAttachedToEngine(FlutterPluginBinding flutterPluginBinding) {
        channel = new MethodChannel(flutterPluginBinding.getFlutterEngine().getDartExecutor(), CHANNEL);
        channel.setMethodCallHandler(this);
    }

    @Override
    public void onDetachedFromEngine(FlutterPluginBinding binding) {
        channel.setMethodCallHandler(null);
    }

    @Override
    public void onMethodCall(MethodCall call, Result result) {
        if (call.method.equals("invoke")) {
            String modelId = call.argument("modelId");
            String prompt = call.argument("prompt");
            Map<String, Object> options = call.argument("options");
            SurrogateModel surrogateModel = new SurrogateModel(modelId);
            SurrogatePrompt surrogatePrompt = new SurrogatePrompt(prompt);
            SurrogateOptions surrogateOptions = new SurrogateOptions(options);
            try {
                String response = surrogateModel.invoke(surrogatePrompt, surrogateOptions);
                result.success(response);
            } catch (Exception e) {
                result.error("UNAVAILABLE", e.getMessage(), null);
            }
        } else {
            result.notImplemented();
        }
    }
}