import { QuickJSContext } from 'quickjs-emscripten';
import { invokeSurrogateAction } from './surrogate-actions';

export class NativeBridge {
  private context: QuickJSContext;

  constructor(context: QuickJSContext) {
    this.context = context;
  }

  exposeToQuickJS() {
    this.context.setProp(this.context.global, 'surrogate', {
      invoke: this.context.newFunction('invoke', (prompt: string, options: any) => {
        try {
          const result = invokeSurrogateAction(prompt, options);
          return this.context.newPromise((resolve, reject) => {
            result.then(resolve).catch(reject);
          });
        } catch (error) {
          throw new Error(`Failed to invoke surrogate action: ${error.message}`);
        }
      })
    });
  }
}