class Polynomial():

    def __init__(self, coefficients):
        """
        Tworzy wielomian o współczynnikach z listy coefficients,
        pozycja w liście oznacza potęgę x, przy którym stoi współczynnik.
        """
        self._coeffs = []
        for i, coefficient in enumerate(coefficients):
            self._coeffs += [coefficient]

    def calculate(self, root):
        sum = self._coeffs[0]
        for i, coefficient in enumerate(self._coeffs):
            if i == 0:
                continue
            else:
                sum += self._coeffs[i]*(root**i)
        return sum

    def is_root(self, root):
        if self.calculate(root):
            return False
        else:
            return True

    def non_zero_coeff(self):
        for coefficient in self._coeffs:
            if coefficient != 0:
                return coefficient

    def probable_integer_roots(self):
        roots = []
        a0 = self.non_zero_coeff()
        for number in range(1, abs(a0)+1):
            if a0//number == a0/number:
                roots += [number, -number]
        return roots

    def integer_roots(self):
        roots = []
        for root in self.probable_integer_roots():
            if self.is_root(root):
                roots += [root]
        if self._coeffs[0] == 0:
            roots.insert(0, 0)
        return roots

    def __repr__(self):
        normal_form = ''
        coeffs_copy = self._coeffs[:]
        coeffs_copy.reverse()
        degree = len(coeffs_copy) - 1
        for i, coefficient in enumerate(coeffs_copy):
            if i == len(coeffs_copy) - 1 and coefficient != 0:
                normal_form += f" {'+' if coefficient > 0 else '-'} {abs(coefficient)}"
            else:
                if coefficient == 0:
                    continue
                elif coefficient > 0:
                    if coefficient == 1:
                        coeff_ = ''
                    else:
                        coeff_ = str(coefficient)
                    if normal_form == '':
                        normal_form +=  f"{coeff_}x^{degree - i}"
                    else:
                        normal_form += f" + {coeff_}x^{degree - i}"
                else:
                    if coefficient == -1:
                        coeff_ = ''
                    else:
                        coeff_ = str(-coefficient)
                    normal_form += f" - {coeff_}x^{degree - i}"
        return normal_form

    def factored_form(self):
        factored_form = ''
        for root in self.integer_roots():
            if root == 0:
                factored_form = "x"
            else:
                buffor = f"(x{'-' if root > 0 else '+'}{abs(root)})"
                factored_form = buffor + factored_form
        if self.lead_coeff()[0] != 1:
            factored_form = str(self.lead_coeff()[0]) + factored_form
        return factored_form

    def lead_coeff(self): 
        list_copy = self._coeffs[:]
        list_copy.reverse()
        for i, coefficient in enumerate(list_copy):
            if coefficient != 0:
                return coefficient, i

if __name__ == "__main__":
    polynomial_1 = Polynomial([0, 12, 10, 2])
    print(polynomial_1)
    print(polynomial_1.integer_roots())
    print(polynomial_1.is_root(0))
    print(polynomial_1.is_root(-1))
    print(polynomial_1.is_root(-2))
    print(polynomial_1.calculate(2))
    print(polynomial_1.factored_form())

    print('')

    polynomial_2 = Polynomial([-6, 1, 4, 1, 0])
    print(polynomial_2)
    print(polynomial_2.integer_roots())
    print(polynomial_2.is_root(0))
    print(polynomial_2.is_root(1))
    print(polynomial_2.is_root(-2))
    print(polynomial_2.calculate(-3))
    print(polynomial_2.factored_form())

    print('')

    polynomial_3 = Polynomial([-24, 34, -7, -4, 1])
    print(polynomial_3)
    print(polynomial_3.integer_roots())
    print(polynomial_3.is_root(0))
    print(polynomial_3.is_root(1))
    print(polynomial_3.is_root(-2))
    print(polynomial_3.calculate(-3))
    print(polynomial_3.factored_form())

    print('')

    polynomial_4 = Polynomial([0, 1, -1, -2, 2, 0, 7, -2, 0])
    print(polynomial_4)
    print(polynomial_4.integer_roots())
    print(polynomial_4.is_root(0))
    print(polynomial_4.is_root(1))
    print(polynomial_4.is_root(-2))
    print(polynomial_4.calculate(-3))
    print(polynomial_4.factored_form())
    