### Modern Scientific Calculator: Sleek Dark‑Theme Calculator with History

This is a Python script for a modern scientific calculator with a sleek, dark‑theme graphical interface. Perform complex calculations with trigonometric functions, switch between degrees and radians, and review your calculation history — all in a visually appealing, user‑friendly app!


#### 🌟 What I Learned

**GUI Development with tkinter:** How to build a complete, professional‑looking graphical user interface using `tkinter` and `ttk`, including labels, buttons, listboxes, and frames with custom styling.


**Modern UI Styling:** How to create a cohesive dark theme with custom button styles, hover effects, and color schemes using `ttk.Style()`.

**Event Handling:** How to bind button clicks to specific functions and manage UI state transitions (e.g., toggling the history panel).


**Scientific Calculations:** How to implement trigonometric functions (`sin`, `cos`, `tan`, `cot`) with support for both degrees and radians, including handling edge cases (e.g., division by zero in `tan` and `cot`).

**Input and State Management:** How to track and manage calculator state (current value, previous value, operator, waiting flag) and handle number input, operators, and special functions.

**History System:** How to maintain and display a calculation history with:
* a toggleable history panel;
* storage of expressions and results;
* display of the last 10 entries;
* ability to clear the entire history.

**Error Handling:** How to catch and display user‑friendly error messages using `try‑except` blocks, ensuring the calculator remains responsive even when invalid operations are attempted.

**String and Operator Mapping:** How to:
* format display text with proper operators (×, ÷) vs. Python operators (*, /);
* convert between display and computational formats using mapping functions (`_map_operator`, `_map_display_operator`).

**User Experience (UX) Design:** How to enhance usability with:
* visual feedback (button hover and press effects);
* clear visual hierarchy (color‑coded buttons for different functions);
* an indicator for angle mode (DEG);
* intuitive layout and responsive design.

---

#### 🚀 How to Use It

1. Run the `modern_scientific_calculator.py` script using Python.
2. A window titled **«Modern Scientific Calculator»** will appear.
3. **Enter numbers** using the numeric keypad (0–9) and the decimal point (.).
4. **Perform operations:**
   * Select an operator (+, −, ×, ÷).
   * Enter the second number.
   * Press «=» to get the result.
5. **Use scientific functions:** Click `sin`, `cos`, `tan`, or `cot` to apply the function to the current number. Click `π` to insert the pi constant.
6. **Access additional functions:**
   * «C» — clear everything;
   * «±» — toggle the sign of the current number;
   * «%» — convert the number to a percentage (divide by 100).
7. **View and manage history:**
   * Click «📋 History» to open the history panel and see the last 10 calculations.
   * Use «Clear All» to erase the entire history.
   * Click «⌨️ Calculator» to return to the main calculator view.

---

#### 🔍 Known Issues & Limitations

* **Security Risk with `eval`:** The calculator uses `eval()` to perform calculations, which can be unsafe with untrusted input. A safer parser should be implemented for production use.
* **No Angle Mode Switch:** The `degrees_mode` flag exists, but there’s no UI element to switch between DEG and RAD.
* **In‑Memory History:** The calculation history is stored only in memory and is lost when the application closes.
* **Precision Handling:** Results are formatted with `f"{result:.8g}"`, which may round very large or very small numbers.
* **Input Validation:** Some invalid inputs may not be caught before conversion to `float`, potentially causing `ValueError`.
* **Performance:** Complex calculations or very large numbers may cause temporary UI freezes without a progress indicator.
* **Fixed Window Size:** The window size is fixed (500×650 px), which may not be optimal for all screen sizes.
* **Limited Error Context:** Error messages are generic («Error») and don’t specify the exact issue.

---

#### 🛫 Try It Yourself

1. Download the `modern_scientific_calculator.py` file.
2. Open it in a Python environment (like IDLE, VS Code, or PyCharm).
3. Run the script. The sleek, dark‑themed calculator window will launch immediately.
4. Test it with different calculations:
   * Try `45`, then click `sin` — you’ll see `sin(45°) = 0.7071068` (in DEG mode).
   * Calculate `2 + 3 × 4` step by step.
   * Insert `π` and see the full value of $\pi$.
   * Compute `5 %` to get `0.05`.
   * Toggle the history panel with «📋 History» and review your past calculations.
5. Explore the interface:
   * Hover over buttons to see the smooth color transitions.
   * Clear everything with «C» or by restarting.
   * Observe how the display updates in real time.

See how the code connects the UI elements to the calculation logic and enjoy your new modern scientific tool!

