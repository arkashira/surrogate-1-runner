import moment from 'moment';

export const formatDate = (date) => {
  return moment(date).format('MMM YYYY');
};

export const isValidDateRange = (startDate, endDate) => {
  const start = moment(startDate);
  const end = moment(endDate);

  return start.isValid() && end.isValid() && !start.isAfter(end);
};

export const formatDateRange = (dateRange) => {
  switch (dateRange) {
    case '7-day':
      return {
        startDate: moment().subtract(7, 'days').format('YYYY-MM-DD'),
        endDate: moment().format('YYYY-MM-DD'),
      };
    case '30-day':
      return {
        startDate: moment().subtract(30, 'days').format('YYYY-MM-DD'),
        endDate: moment().format('YYYY-MM-DD'),
      };
    default:
      const [start, end] = dateRange.split('-').map(date => moment(date).format('YYYY-MM-DD'));
      return { startDate: start, endDate: end };
  }
};