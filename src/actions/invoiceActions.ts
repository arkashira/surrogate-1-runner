import { Dispatch } from 'redux';
import { InvoiceSummary } from '../types';
import { fetchInvoiceSummaries as fetchSummaries } from '../api/invoiceApi';

export const FETCH_INVOICE_SUMMARIES_REQUEST = 'FETCH_INVOICE_SUMMARIES_REQUEST';
export const FETCH_INVOICE_SUMMARIES_SUCCESS = 'FETCH_INVOICE_SUMMARIES_SUCCESS';
export const FETCH_INVOICE_SUMMARIES_FAILURE = 'FETCH_INVOICE_SUMMARIES_FAILURE';

export const fetchInvoiceSummaries = () => {
  return async (dispatch: Dispatch) => {
    dispatch({ type: FETCH_INVOICE_SUMMARIES_REQUEST });
    try {
      const summaries: InvoiceSummary[] = await fetchSummaries();
      dispatch({ type: FETCH_INVOICE_SUMMARIES_SUCCESS, payload: summaries });
    } catch (error) {
      dispatch({ type: FETCH_INVOICE_SUMMARIES_FAILURE, payload: error.message });
    }
  };
};