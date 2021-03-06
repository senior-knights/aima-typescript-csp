import { Problem } from "../src";

describe("search object instance", () => {
  const problem = new Problem(1);
  it("is initialized", () => {
    expect(problem.initial).toEqual(1);
    expect(problem.goal).toEqual(undefined);
  });

  it("throws on action()", () => {
    expect(() => problem.action(-1)).toThrow("Not Implemented");
  });

  it("throws on result()", () => {
    expect(() => problem.result(1, undefined)).toThrow("Not Implemented");
  });

  it("correctly assesses goals with goal_test()", () => {
    expect(problem.goal_test(-1));

    problem.goal = 1;
    expect(problem.goal_test(-1)).not.toEqual(true);
    expect(problem.goal_test(1));

    problem.goal = [1, 2];
    expect(problem.goal_test(-1)).not.toEqual(true);
    expect(problem.goal_test(2));
  });

  it("correctly calculates path_cost()", () => {
    expect(problem.path_cost(1, -1, undefined, -1)).toEqual(2);
    expect(problem.path_cost(10, -1, undefined, -1)).toEqual(11);
  });

  it("throws on value()", () => {
    expect(() => problem.value(-1)).toThrow("Not Implemented");
  });
});
