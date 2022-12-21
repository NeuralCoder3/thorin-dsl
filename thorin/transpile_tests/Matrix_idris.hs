matrixMultiply : (m : Nat) -> (n : Nat) -> (p : Nat) -> 
                (matrix m n) -> (matrix n p) -> matrix m p
matrixMultiply m n p mat1 mat2 = 
  let 
    multRow : (row : Vec n Nat) -> (matrix n p) -> Vec p Nat
    multRow row mat = 
      let 
        multElem : (elem : Nat) -> (col : Vec p Nat) -> Nat
        multElem elem col = elem * (head col) + (multElem (tail row) (tail col))
      in 
        multElem (head row) (head mat) :: multRow (tail row) (tail mat)
  in 
    case mat1 of 
      [] => []
      row :: rows => multRow row mat2 :: matrixMultiply m n p rows mat2
