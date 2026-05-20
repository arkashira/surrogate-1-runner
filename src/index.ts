import { QuickJSContext } from 'quickjs-emscripten';
import { NativeBridge } from './native-bridge';

async function main() {
  const context = await QuickJSContext.create();
  const nativeBridge = new NativeBridge(context);
  nativeBridge.exposeToQuickJS();

  // Example usage
  const jsCode = `
    surrogate.invoke('Hello, world!', { option1: 'value1' })
      .then(response => console.log(response))
      .catch(error => console.error(error));
  `;

  await context.evalCode(jsCode);
  await context.dispose();
}

main().catch(console.error);