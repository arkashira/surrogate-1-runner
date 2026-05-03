   // quick test in Node/ts-node
   import { validateTransition, TERMINAL_STATUSES } from './models/transition';

   // valid
   console.log(validateTransition(null, 'submitted', 'user@x.com', 'initial submit'));

   // invalid: terminal -> non-terminal
   try {
     validateTransition('closed', 'submitted', 'user@x.com', 'reopen');
   } catch (e) {
     console.log(e.message); // expected
   }