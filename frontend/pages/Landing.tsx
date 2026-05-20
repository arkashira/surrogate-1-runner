import { useRouter } from 'next/router';
import Head from 'next/head';

const Landing: React.FC = () => {
  const router = useRouter();

  const handleGetStarted = () => {
    router.push('/signup');
  };

  const handleLogin = () => {
    router.push('/login');
  };

  return (
    <>
      <Head>
        <title>Welcome to Axentx Surrogate</title>
        <meta name="description" content="Start managing your data efficiently with Axentx." />
      </Head>

      <main style={styles.container}>
        <h1 style={styles.title}>Welcome to Axentx</h1>
        <p style={styles.subtitle}>Start managing your data efficiently.</p>

        <button style={styles.ctaButton} onClick={handleGetStarted}>
          Get Started
        </button>

        <p style={styles.loginPrompt}>
          Already have an account?{' '}
          <button style={styles.loginLink} onClick={handleLogin}>
            Log in
          </button>
        </p>
      </main>
    </>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f7fa',
    padding: '0 1rem',
    textAlign: 'center',
  },
  title: {
    fontSize: '2.5rem',
    marginBottom: '0.5rem',
    color: '#333',
  },
  subtitle: {
    fontSize: '1.25rem',
    marginBottom: '2rem',
    color: '#555',
  },
  ctaButton: {
    backgroundColor: '#0066ff',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    padding: '0.75rem 1.5rem',
    fontSize: '1rem',
    cursor: 'pointer',
    transition: 'background-color 0.2s ease',
  },
  loginPrompt: {
    marginTop: '1.5rem',
    fontSize: '0.9rem',
    color: '#666',
  },
  loginLink: {
    color: '#0066ff',
    textDecoration: 'none',
    cursor: 'pointer',
  },
};

export default Landing;