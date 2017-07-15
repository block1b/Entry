function l = loop(array, len)
    for j=1:len
        l(j) = array{j}.timestamp_low;
    end
end
