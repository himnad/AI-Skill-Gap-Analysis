"use client";

import { useEffect, useState } from "react";

type Recommendation = {
  course_name: string;
  discipline: string;
  instructor: string;
  institute: string;
  course_url: string;
  similarity_score: number;
};

type AnalysisResult = {
  resume_skills: string[];
  missing_skills: string[];
  recommendations: Recommendation[];
};

// Uses the production API URL on Vercel.
// Falls back to the local FastAPI server during local development.
const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export default function Home() {
  const [darkMode, setDarkMode] = useState(false);

  const [resume, setResume] = useState<File | null>(null);
  const [jobDescription, setJobDescription] =
    useState<File | null>(null);

  const [result, setResult] =
    useState<AnalysisResult | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Load saved night-mode preference.
  useEffect(() => {
    const savedMode = localStorage.getItem("darkMode");

    if (savedMode === "true") {
      setDarkMode(true);
    }
  }, []);

  // Save night-mode preference.
  useEffect(() => {
    localStorage.setItem("darkMode", String(darkMode));
  }, [darkMode]);

  // Send the uploaded PDFs to the FastAPI backend.
  const analyzeSkills = async () => {
    if (!resume || !jobDescription) {
      setError(
        "Please upload both your resume and job description."
      );
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();

    formData.append("resume", resume);
    formData.append("job_description", jobDescription);

    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(
          "Analysis failed. Please try again."
        );
      }

      const data: AnalysisResult = await response.json();

      setResult(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main
      className={`min-h-screen transition-colors duration-300 ${
        darkMode
          ? "bg-gray-950 text-white"
          : "bg-white text-gray-900"
      }`}
    >
      {/* Header */}
      <header
        className={`border-b ${
          darkMode
            ? "border-gray-800 bg-gray-950"
            : "border-gray-200 bg-white"
        }`}
      >
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
          <div>
            <h1 className="text-xl font-bold">
              AI Skill Gap Analysis
            </h1>

            <p
              className={`text-sm ${
                darkMode
                  ? "text-gray-400"
                  : "text-gray-500"
              }`}
            >
              Resume & Job Description Analyzer
            </p>
          </div>

          {/* Night Mode Toggle */}
          <button
            onClick={() => setDarkMode(!darkMode)}
            className={`rounded-full border px-4 py-2 text-sm font-medium transition ${
              darkMode
                ? "border-gray-700 bg-gray-800 text-white hover:bg-gray-700"
                : "border-gray-300 bg-gray-100 text-gray-900 hover:bg-gray-200"
            }`}
          >
            {darkMode
              ? "☀️ Light Mode"
              : "🌙 Night Mode"}
          </button>
        </div>
      </header>

      {/* Main Section */}
      <section className="mx-auto max-w-6xl px-6 py-16">
        <div className="text-center">
          <h2 className="text-4xl font-bold tracking-tight">
            Discover Your Skill Gaps
          </h2>

          <p
            className={`mx-auto mt-4 max-w-2xl text-lg ${
              darkMode
                ? "text-gray-400"
                : "text-gray-600"
            }`}
          >
            Upload your resume and a job description to
            identify missing skills and discover relevant
            NPTEL courses.
          </p>
        </div>

        {/* Upload Cards */}
        <div className="mt-12 grid gap-6 md:grid-cols-2">
          {/* Resume */}
          <div
            className={`rounded-xl border p-8 ${
              darkMode
                ? "border-gray-800 bg-gray-900"
                : "border-gray-200 bg-gray-50"
            }`}
          >
            <h3 className="text-lg font-semibold">
              📄 Resume
            </h3>

            <p
              className={`mt-2 text-sm ${
                darkMode
                  ? "text-gray-400"
                  : "text-gray-500"
              }`}
            >
              Upload your resume in PDF format.
            </p>

            <div
              className={`mt-6 rounded-lg border-2 border-dashed p-8 text-center ${
                darkMode
                  ? "border-gray-700"
                  : "border-gray-300"
              }`}
            >
              <input
                type="file"
                accept=".pdf"
                onChange={(event) => {
                  setResume(
                    event.target.files?.[0] ?? null
                  );
                }}
                className="block w-full text-sm"
              />

              {resume && (
                <p className="mt-3 text-sm font-medium">
                  Selected: {resume.name}
                </p>
              )}
            </div>
          </div>

          {/* Job Description */}
          <div
            className={`rounded-xl border p-8 ${
              darkMode
                ? "border-gray-800 bg-gray-900"
                : "border-gray-200 bg-gray-50"
            }`}
          >
            <h3 className="text-lg font-semibold">
              💼 Job Description
            </h3>

            <p
              className={`mt-2 text-sm ${
                darkMode
                  ? "text-gray-400"
                  : "text-gray-500"
              }`}
            >
              Upload the job description in PDF format.
            </p>

            <div
              className={`mt-6 rounded-lg border-2 border-dashed p-8 text-center ${
                darkMode
                  ? "border-gray-700"
                  : "border-gray-300"
              }`}
            >
              <input
                type="file"
                accept=".pdf"
                onChange={(event) => {
                  setJobDescription(
                    event.target.files?.[0] ?? null
                  );
                }}
                className="block w-full text-sm"
              />

              {jobDescription && (
                <p className="mt-3 text-sm font-medium">
                  Selected: {jobDescription.name}
                </p>
              )}
            </div>
          </div>
        </div>

        {/* Analyze Button */}
        <div className="mt-8 text-center">
          <button
            onClick={analyzeSkills}
            disabled={loading}
            className="rounded-lg bg-black px-8 py-3 font-semibold text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-white dark:text-black dark:hover:bg-gray-200"
          >
            {loading
              ? "Analyzing..."
              : "Analyze Skill Gap"}
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mx-auto mt-6 max-w-3xl rounded-lg border border-red-300 bg-red-50 p-4 text-center text-sm text-red-700">
            {error}
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="mt-16 space-y-8">
            {/* Resume Skills */}
            <section
              className={`rounded-xl border p-8 ${
                darkMode
                  ? "border-gray-800 bg-gray-900"
                  : "border-gray-200 bg-gray-50"
              }`}
            >
              <h3 className="text-2xl font-bold">
                Resume Skills
              </h3>

              <div className="mt-5 flex flex-wrap gap-2">
                {result.resume_skills.map(
                  (skill, index) => (
                    <span
                      key={`${skill}-${index}`}
                      className={`rounded-full px-3 py-1 text-sm ${
                        darkMode
                          ? "bg-gray-800 text-gray-200"
                          : "border border-gray-200 bg-white text-gray-700"
                      }`}
                    >
                      {skill}
                    </span>
                  )
                )}
              </div>
            </section>

            {/* Missing Skills */}
            <section
              className={`rounded-xl border p-8 ${
                darkMode
                  ? "border-gray-800 bg-gray-900"
                  : "border-gray-200 bg-gray-50"
              }`}
            >
              <h3 className="text-2xl font-bold">
                Skill Gaps
              </h3>

              {result.missing_skills.length === 0 ? (
                <p className="mt-4">
                  No significant skill gaps were
                  identified.
                </p>
              ) : (
                <div className="mt-5 flex flex-wrap gap-3">
                  {result.missing_skills.map(
                    (skill, index) => (
                      <span
                        key={`${skill}-${index}`}
                        className="rounded-full bg-red-100 px-4 py-2 text-sm font-medium text-red-700"
                      >
                        {skill}
                      </span>
                    )
                  )}
                </div>
              )}
            </section>

            {/* Recommended Courses */}
            <section>
              <h3 className="text-2xl font-bold">
                Recommended NPTEL Courses
              </h3>

              <div className="mt-6 grid gap-5">
                {result.recommendations.map(
                  (course, index) => (
                    <div
                      key={`${course.course_name}-${index}`}
                      className={`rounded-xl border p-6 ${
                        darkMode
                          ? "border-gray-800 bg-gray-900"
                          : "border-gray-200 bg-white"
                      }`}
                    >
                      <div className="flex flex-col justify-between gap-4 md:flex-row">
                        <div>
                          <p className="text-sm font-medium text-gray-500">
                            Recommendation #
                            {index + 1}
                          </p>

                          <h4 className="mt-1 text-xl font-semibold">
                            {course.course_name}
                          </h4>

                          <p
                            className={`mt-2 text-sm ${
                              darkMode
                                ? "text-gray-400"
                                : "text-gray-600"
                            }`}
                          >
                            {course.institute} •{" "}
                            {course.instructor}
                          </p>

                          <p
                            className={`mt-1 text-sm ${
                              darkMode
                                ? "text-gray-400"
                                : "text-gray-600"
                            }`}
                          >
                            {course.discipline}
                          </p>
                        </div>

                        <div className="flex flex-col items-start gap-3 md:items-end">
                          <span
                            className={`rounded-full px-3 py-1 text-sm font-medium ${
                              darkMode
                                ? "bg-gray-800"
                                : "bg-gray-100"
                            }`}
                          >
                            Similarity:{" "}
                            {course.similarity_score}
                          </span>

                          <a
                            href={course.course_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="font-medium underline"
                          >
                            View Course →
                          </a>
                        </div>
                      </div>
                    </div>
                  )
                )}
              </div>
            </section>
          </div>
        )}
      </section>
    </main>
  );
}