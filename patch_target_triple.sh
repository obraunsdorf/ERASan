find . -type f -name "*.sh" | while read -r file; do
    if grep -q "x86_64-unknown-linux-gnu" "$file"; then
        if head -n 1 "$file" | grep -q "^#!"; then
            sed -i '1a TARGETTRIPLE=$(uname -m)-unknown-linux-gnu' "$file"
        else
            sed -i '1i TARGETTRIPLE=$(uname -m)-unknown-linux-gnu' "$file"
        fi
        sed -i 's/x86_64-unknown-linux-gnu/$TARGETTRIPLE/g' "$file"
    fi
done
