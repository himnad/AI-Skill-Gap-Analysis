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
