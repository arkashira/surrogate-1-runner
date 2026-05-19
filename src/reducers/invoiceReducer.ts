import { InvoiceSummary } from '../types';
import {
  FETCH_INVOICE_SUMMARIES_REQUEST,
  FETCH_INVOICE_SUMMARIES_SUCCESS,
  FETCH_INVOICE_SUMMARIES_FAILURE,
} from '../actions/invoiceActions';

interface InvoiceState {
  invoiceSummaries: InvoiceSummary[];
  loading: boolean;
  error: string | null;
}

const initialState: InvoiceState = {
  invoiceSummaries: [],
  loading: false,
  error: null,
};

const invoiceReducer = (state = initialState, action: any) => {
  switch (action.type) {
    case FETCH_INVOICE_SUMMARIES_REQUEST:
      return {
        ...state,
        loading: true,
        error: null,
      };
    case FETCH_INVOICE_SUMMARIES_SUCCESS:
      return {
        ...state,
        loading: false,
        invoiceSummaries: action.payload,
      };
    case FETCH_INVOICE_SUMMARIES_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.payload,
      };
    default:
      return state;
  }
};

export default invoiceReducer;