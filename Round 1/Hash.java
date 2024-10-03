import java.util.*;
public class Hash {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String input = sc.next();
        String longestPalindrome = longestPalindrome(input);
        System.out.println("Longest Palindrome Substring: " + longestPalindrome);
    }
    public static String longestPalindrome(String s) {
        String result = "";
        int resLen = 0;

        for (int i = 0; i < s.length(); i++) {
            int l = i, r = i;
            while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) {
                if (r - l + 1 > resLen) {
                    result = s.substring(l, r + 1);
                    resLen = r - l + 1;
                }
                l--;
                r++;
            }

            l = i;
            r = i + 1;
            while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) {
                if (r - l + 1 > resLen) {
                    result = s.substring(l, r + 1);
                    resLen = r - l + 1;
                }
                l--;
                r++;
            }
        }

        return result;
    }
}
