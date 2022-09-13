import Head from 'next/head'
import Layout from '@/components/Layout/Layout'
import styles from '@/styles/about.module.css'

export default function aboutPage() {
  return (
    <Layout>
      <Head>
        <title>Coursaholic | Organizations</title>
        {/* Change this icon when we have a logo */}
        <link rel="icon" href="/CoursaholicLogo.svg" />
      </Head>
      <section className={styles.content}>
        <h1>About Us</h1>
        <p>
          Founded <strong>October 2021 🧑‍💻.</strong>
        </p>
        <p>
          Developed at the <strong>University of California, Riverside.</strong>
        </p>
        <p>
          Coursaholic was made with the intent to{' '}
          <strong>provide equal power for all students to sign up for the academic courses they wanted.</strong>
        </p>
        <p>
          Information on classes, clubs, and organizations span many different
          sites and media that students may not always be following. Coursaholic aims
          to provide a single place where students are able to find the
          information they need. From class reviews and info to club posts and
          events, Coursaholic is <i>where information gathers</i>.
        </p>
        <p>
          Developed with a passion for improving lives and disrupting the world by,
          <br />
          <br />
         Dylan Nguyen
          <br />
          <a
            rel="noopener noreferrer"
            href="https://dylanhnguyen.com"
            target="_blank"
          >
            Dylan Nguyen
          </a>
          <br />
        </p>
      </section>
    </Layout>
  )
}
