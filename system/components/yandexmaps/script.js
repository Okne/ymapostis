ymaps.ready(init);

        function init () {
            var myMap = new ymaps.Map("map", {
                    center: [55.76, 37.64],
                    zoom: 10
                });

            myMap.balloon.open(
                // ������� ������
                [55.76, 37.64], {
                    // �������� ������
                    contentBody: '������'
                }, {
                    // ����� ������. � ������ ������� ���������, ��� ����� �� ������ ����� ������ ��������.
                    closeButton: false
                });
        }