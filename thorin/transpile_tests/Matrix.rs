fn main() {
    // Create two matrices to be multiplied
    let matrix_a = [[1, 2], [3, 4]];
    let matrix_b = [[5, 6], [7, 8]];

    // Initialize a result matrix with the same number of rows as matrix A and the same number of columns as matrix B
    let mut result = [[0; 2]; 2];

    // Iterate over the rows of matrix A
    for i in 0..2 {
        // Iterate over the columns of matrix B
        for j in 0..2 {
            // Initialize the element of the result matrix to 0
            result[i][j] = 0;

            // Iterate over the rows of matrix B (which is also the number of columns in matrix A)
            for k in 0..2 {
                // Multiply the elements of the current row of matrix A by the elements of the current column of matrix B and add them to the result
                result[i][j] += matrix_a[i][k] * matrix_b[k][j];
            }
        }
    }

    // Print the result matrix
    println!("{:?}", result);
}
