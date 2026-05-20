import ReactGA from 'react-ga';

ReactGA.initialize('UA-XXXXX-X'); // Replace with your Google Analytics Tracking ID

export const logPageView = () => {
  ReactGA.set({ page: window.location.pathname });
  ReactGA.pageview(window.location.pathname);
};

export const logEvent = (category, action, label) => {
  ReactGA.event({ category, action, label });
};